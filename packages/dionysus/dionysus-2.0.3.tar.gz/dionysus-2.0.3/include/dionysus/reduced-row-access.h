#ifndef DIONYSUS_REDUCED_ROW_ACCESS_H
#define DIONYSUS_REDUCED_ROW_ACCESS_H

#include <vector>
#include <tuple>

#include <boost/intrusive/list.hpp>
namespace bi = boost::intrusive;

#include "reduced-matrix.h"

namespace dionysus
{

namespace detail
{
    typedef     bi::list_base_hook<bi::link_mode<bi::auto_unlink>>      auto_unlink_hook;

    template<class Field, class Index, class Cmp>
    struct SparseRowEntry: public ChainEntry<Field, Index, auto_unlink_hook>
    {
        typedef             ChainEntry<Field, Index, auto_unlink_hook>          Parent;

                            Entry(FieldElement e, const Index& i, ColumnsIterator it):
                                Parent(e,i), column(it)                         {}

                            Entry(const Entry& other) = default;
                            Entry(Entry&& other) = default;

        void                unlink()                                            { auto_unlink_hook::unlink(); }
        bool                is_linked()  const                                  { return auto_unlink_hook::is_linked();  }

        ColumnsIterator     column;     // TODO: I really don't like this overhead
    };
}

// FIXME: Index needs to be a pair, with one being an iterator
template<class Field_, typename Index_ = unsigned, class Comparison_ = std::less<Index_>, template<class Self> class... Visitors>
class ReducedRowAccess:
    public ReducedMatrix<Field_, Index_, Comparison_,
                         detail::SparseRowEntry<Field_, Index_, Comparison_>,
                         Visitors...>          // TODO: add the necessary visitor
{
        // FIXME: copied directly from CohomologyPersistence
        struct      Entry;
        struct      ColumnHead;

        typedef     std::vector<Entry>                                      Column;
        typedef     bi::list<Entry, bi::constant_time_size<false>>          Row;
        typedef     std::list<ColumnHead>                                   Columns;
        typedef     typename Columns::iterator                              ColumnsIterator;

};

}

#endif
